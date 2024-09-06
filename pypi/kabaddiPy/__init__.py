from .kabaddiPy import KabaddiDataAPI

# Automatically instantiate KabaddiDataAPI and expose it as 'api'
kabaddiPy = KabaddiDataAPI()

# Optional: Expose KabaddiDataAPI class in case users still want to instantiate it manually
__all__ = ['kabaddiPy', 'KabaddiDataAPI']