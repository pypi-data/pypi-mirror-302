"""
epic_fourier - A library for computing Fourier coefficients.

This package provides tools to compute Fourier coefficients for periodic functions.
"""
__version__ = '0.1.0'

import logging

logging.basicConfig(
    level=logging.INFO,  # Adjust to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fourier_series.log"),  # Log to a file
        logging.StreamHandler()
    ]
)   

logger = logging.getLogger(__name__)
logger.info('epic_fourier package initialized, have fun :)')
