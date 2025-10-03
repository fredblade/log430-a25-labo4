"""
Centralized logging configuration for the application
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs: Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import logging
import sys

class Logger:
    """Centralized logger configuration"""
    
    @staticmethod
    def start(name: str, level=logging.DEBUG):
        """ Set up a logger with both console and file handlers """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False
        
        # Prevent duplicate handlers if logger already exists
        if logger.handlers:
            return logger
        
        # Format for logs
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Ensure root logger doesn't interfere
        logging.root.setLevel(logging.WARNING)
        
        return logger