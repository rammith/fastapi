from main import about, home


def test_home_endpoint():
    assert home() == {"message": "Hello Obito"}


def test_about_endpoint():
    assert about() == {"message": "About Page"}
