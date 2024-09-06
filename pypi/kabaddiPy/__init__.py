from .kabaddiPy import PKL

# Automatically instantiate KabaddiDataAPI and expose it as 'api'
pkl = PKL()

# Optional: Expose KabaddiDataAPI class in case users still want to instantiate it manually
__all__ = ['pkl', 'PKL']