@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []

    inventories = db.session.query(Inventory).join(Warehouse).filter(
        Warehouse.company_id == company_id
    ).all()

    for inv in inventories:
        product = inv.product

        # Skip if no recent sales
        if not product.has_recent_sales(days=30):
            continue

        threshold = product.get_low_stock_threshold()

        if inv.quantity < threshold:
            avg_daily_sales = product.get_avg_daily_sales()
            days_until_stockout = (
                inv.quantity // avg_daily_sales if avg_daily_sales > 0 else None
            )

            supplier = product.suppliers[0] if product.suppliers else None

            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": inv.warehouse.id,
                "warehouse_name": inv.warehouse.name,
                "current_stock": inv.quantity,
                "threshold": threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": {
                    "id": supplier.id,
                    "name": supplier.name,
                    "contact_email": supplier.contact_email
                } if supplier else None
            })

    return {
        "alerts": alerts,
        "total_alerts": len(alerts)
    }
