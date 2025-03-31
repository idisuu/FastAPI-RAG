import logging
from app.core.configs.config import main_config

# ✅ 전역 로거 생성
logger = logging.getLogger("app_logger")
logger.setLevel(getattr(logging, main_config.LOG_LEVEL, logging.INFO))  # 환경 변수에서 설정된 로그 레벨 사용

# ✅ 로그 포맷 설정
log_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] - %(message)s"
)

# ✅ 콘솔 핸들러 추가
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)