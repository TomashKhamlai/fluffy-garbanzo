from app.controllers.assets_controller import AssetsController
from app.controllers.index_controller import IndexController
from app.controllers.product_controller import ProductController


def setup_routing(app_instance) -> None:
    # Instantiate controllers
    assets_controller = AssetsController()
    index_controller = IndexController()
    product_controller = ProductController()

    # Define routes and bind them to the instance methods
    app_instance.route(
        '/',
        callback=assets_controller.get_index,
        name='index'
    )

    app_instance.route(
        '/products',
        callback=index_controller.get_products,
        name='index'
    )

    app_instance.route(
        '/favicon.ico',
        callback=assets_controller.get_favicon,
        name='static'
    )

    app_instance.route(
        '/qr-images/<filename>',
        callback=assets_controller.get_qr_code,
        name='static'
    )

    app_instance.route(
        '/product', method='GET',
        callback=product_controller.get_product,
        name='product'
    )

    app_instance.route(
        '/product/<uuid_str>', method='GET',
        callback=product_controller.get_product,
        name='product'
    )

    app_instance.route(
        '/product', method='POST',
        callback=product_controller.create_product,
        name='product'
    )
    app_instance.route(
        '/product/<uuid_str>', method='DELETE',
        callback=product_controller.delete_product,
        name='product'
    )
