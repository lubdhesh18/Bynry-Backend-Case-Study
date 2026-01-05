@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # Basic validation
    required_fields = ['name', 'sku', 'price']
    for field in required_fields:
        if field not in data:
            return {"error": f"{field} is required"}, 400

    # SKU uniqueness check
    existing_product = Product.query.filter_by(sku=data['sku']).first()
    if existing_product:
        return {"error": "SKU already exists"}, 409

    try:
        # Start transaction
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=Decimal(data['price'])
        )
        db.session.add(product)
        db.session.flush()  # Get product.id without committing

        # Create inventory only if warehouse info is provided
        if 'warehouse_id' in data and 'initial_quantity' in data:
            inventory = Inventory(
                product_id=product.id,
                warehouse_id=data['warehouse_id'],
                quantity=data['initial_quantity']
            )
            db.session.add(inventory)

        db.session.commit()

        return {
            "message": "Product created successfully",
            "product_id": product.id
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to create product"}, 500
