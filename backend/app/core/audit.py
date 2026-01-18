"""
Security Audit Logging

Centralized logging for security-related events.
"""
from loguru import logger
from datetime import datetime, timezone
from typing import Optional


class AuditLogger:
    """Centralized audit logging for security events."""

    @staticmethod
    def login_success(username: str, ip_address: str, user_agent: Optional[str] = None):
        """Log successful login attempt."""
        logger.info(
            f"[AUDIT] LOGIN_SUCCESS | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"user_agent={user_agent or 'unknown'} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def login_failure(username: str, ip_address: str, reason: str = "invalid_credentials"):
        """Log failed login attempt."""
        logger.warning(
            f"[AUDIT] LOGIN_FAILURE | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"reason={reason} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def account_locked(username: str, ip_address: str, failed_attempts: int):
        """Log account lockout event."""
        logger.warning(
            f"[AUDIT] ACCOUNT_LOCKED | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"failed_attempts={failed_attempts} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def account_unlocked(username: str, method: str = "automatic"):
        """Log account unlock event."""
        logger.info(
            f"[AUDIT] ACCOUNT_UNLOCKED | "
            f"user={username} | "
            f"method={method} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def password_changed(username: str, ip_address: str):
        """Log password change event."""
        logger.info(
            f"[AUDIT] PASSWORD_CHANGED | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def token_refresh(username: str, ip_address: str):
        """Log token refresh event."""
        logger.info(
            f"[AUDIT] TOKEN_REFRESH | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def token_reuse_detected(username: str, ip_address: str):
        """Log potential token reuse attack."""
        logger.error(
            f"[AUDIT] TOKEN_REUSE_DETECTED | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def logout(username: str, ip_address: str):
        """Log logout event."""
        logger.info(
            f"[AUDIT] LOGOUT | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def registration(username: str, ip_address: str):
        """Log new user registration."""
        logger.info(
            f"[AUDIT] USER_REGISTERED | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def privilege_escalation_attempt(username: str, ip_address: str, attempted_action: str):
        """Log privilege escalation attempt."""
        logger.critical(
            f"[AUDIT] PRIVILEGE_ESCALATION_ATTEMPT | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"action={attempted_action} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def unauthorized_access_attempt(username: str, ip_address: str, resource: str):
        """Log unauthorized access attempt."""
        logger.warning(
            f"[AUDIT] UNAUTHORIZED_ACCESS | "
            f"user={username} | "
            f"ip={ip_address} | "
            f"resource={resource} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def rate_limit_exceeded(ip_address: str, endpoint: str):
        """Log rate limit exceeded event."""
        logger.warning(
            f"[AUDIT] RATE_LIMIT_EXCEEDED | "
            f"ip={ip_address} | "
            f"endpoint={endpoint} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )

    @staticmethod
    def csrf_validation_failure(ip_address: str, endpoint: str):
        """Log CSRF validation failure."""
        logger.warning(
            f"[AUDIT] CSRF_VALIDATION_FAILURE | "
            f"ip={ip_address} | "
            f"endpoint={endpoint} | "
            f"timestamp={datetime.now(timezone.utc).isoformat()}"
        )
