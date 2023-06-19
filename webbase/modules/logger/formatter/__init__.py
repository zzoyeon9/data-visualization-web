#-*- coding:utf-8 -*-

"""Logger Formatters
"""

__all__ = [
    'ColourizedFormatter',
]

#
# Import modules
#
import uvicorn
import uvicorn.logging

# Formatte
ColourizedFormatter = uvicorn.logging.ColourizedFormatter
