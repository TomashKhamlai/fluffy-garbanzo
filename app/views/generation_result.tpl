<!DOCTYPE html>
<html>
<head>
    <title>QR Code Generation Results</title>
    <style>
        .product-list {
            padding: 0;
        }
        .product-item {
            list-style: none;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .product-info {
            flex: 1;
            text-align: center;
            font-size: 2em
        }
        .product-name {
            letter-spacing: .15em
        }
        .product-image {
            flex: 1;
            display: flex;
            justify-content: flex-end;
        }
    </style>
</head>
<body>
    <h1>QR Code Generation Results</h1>
    % if products:
        <ul class="product-list">
            % for product, image_path in zip(products, images):
                <li class="product-item">
                    <span class="product-info"><span class="product-name">{{ product.name }}</span></span>
                    <div class="product-image">
                        <img src="{{ image_path }}" alt="QR code for {{ product.uuid_str }}" />
                    </div>
                </li>
            % end
        </ul>
    % else:
        <p>No products found.</p>
    % end
</body>
</html>
