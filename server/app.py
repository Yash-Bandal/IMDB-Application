from imdb_api import ApiError, create_app, required_settings, setting

app = create_app()


if __name__ == "__main__":
    if setting("APP_ENV", "development").lower() != "development":
        required_settings()
    app.run(host=setting("HOST", "0.0.0.0"), port=int(setting("PORT", "10000")))


__all__ = ["ApiError", "app", "create_app", "required_settings", "setting"]
