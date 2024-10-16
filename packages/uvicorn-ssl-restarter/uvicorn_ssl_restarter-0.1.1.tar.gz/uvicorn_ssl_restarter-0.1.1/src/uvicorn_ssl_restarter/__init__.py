import asyncio
import os
from datetime import datetime

import OpenSSL
import uvicorn
from loguru import logger


class UvicornSSLRestarter:

    def __init__(
        self,
        app_path="app.main:app",
        fallback_certs_dir="/app/fallback-certs",
        real_certs_dir="/app/certs",
        renew_window_days=7,
        renew_check_interval=60 * 60 * 2,
        server_port=443,
    ):
        self.app_path = app_path
        self.fallback_certs_dir = fallback_certs_dir
        self.real_certs_dir = real_certs_dir
        self.renew_window_days = renew_window_days
        self.renew_check_interval = renew_check_interval
        self.server_port = server_port

    def get_real_cert_path(self):
        virtual_host = os.environ.get("VIRTUAL_HOST")
        ssl_keyfile_path = f"{self.real_certs_dir}/{virtual_host}/privkey.pem"
        ssl_certfile_path = f"{self.real_certs_dir}/{virtual_host}/fullchain.pem"
        return ssl_keyfile_path, ssl_certfile_path

    def get_self_signed_cert_path(self):
        ssl_keyfile_path = f"{self.fallback_certs_dir}/private.key"
        ssl_certfile_path = f"{self.fallback_certs_dir}/certificate.crt"
        return ssl_keyfile_path, ssl_certfile_path

    async def get_ssl_cert_path(self):
        ssl_keyfile_path, ssl_certfile_path = self.get_real_cert_path()
        if not (os.path.isfile(ssl_keyfile_path) and os.path.isfile(ssl_certfile_path)):
            logger.warning("SSL certificate not found. Using self-signed certificate.")
            return self.get_self_signed_cert_path()
        return ssl_keyfile_path, ssl_certfile_path

    async def get_certificate_expiry(self, certificate_path) -> datetime:
        with open(certificate_path, "rb") as cert_file:
            cert_data = cert_file.read()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)
        expiry_date = cert.get_notAfter().decode("ascii")
        return datetime.strptime(expiry_date, "%Y%m%d%H%M%SZ")

    async def https_restart_loop(self, server, current_certificate_expiry):
        """Check SSL certificate expiry every 2 hours and restart server
        if necessary, to activate new certificate."""
        while True:
            logger.info(
                f"Checking SSL expiry in {self.renew_check_interval} seconds..."
            )
            await asyncio.sleep(self.renew_check_interval)
            time_until_expiry = current_certificate_expiry - datetime.now()
            logger.info(f"Time until SSL expiry: {time_until_expiry}")

            if (
                "fallback-certs" not in server.config.ssl_certfile
                and time_until_expiry.days > self.renew_window_days
            ):
                continue

            ssl_keyfile_path, ssl_certfile_path = await self.get_ssl_cert_path()
            new_certificate_expiry = await self.get_certificate_expiry(
                ssl_certfile_path
            )

            if new_certificate_expiry == current_certificate_expiry:
                if time_until_expiry.days <= self.renew_window_days:
                    logger.warning(
                        "Certificate expires soon, but no updated certificate found."
                    )
                logger.info("No updated certificate found. Skipping restart.")
                continue

            logger.info("Restarting server to activate new SSL cert...")

            server.should_exit = True
            await server.shutdown()

            server = await self.start_server(ssl_keyfile_path, ssl_certfile_path)
            current_certificate_expiry = new_certificate_expiry

    async def start_server(self, ssl_keyfile_path, ssl_certfile_path):
        uvicorn_config = uvicorn.Config(
            self.app_path,
            host="0.0.0.0",
            port=self.server_port,
            reload=True,
            ssl_keyfile=ssl_keyfile_path,
            ssl_certfile=ssl_certfile_path,
        )
        server = uvicorn.Server(uvicorn_config)
        asyncio.create_task(server.serve())
        return server

    async def run(self):
        ssl_keyfile_path, ssl_certfile_path = await self.get_ssl_cert_path()
        certificate_expiry = await self.get_certificate_expiry(ssl_certfile_path)
        server = await self.start_server(ssl_keyfile_path, ssl_certfile_path)
        asyncio.create_task(self.https_restart_loop(server, certificate_expiry))
