companies (
  id INT PRIMARY KEY,
  name VARCHAR(255)
);

warehouses (
  id INT PRIMARY KEY,
  company_id INT,
  name VARCHAR(255),
  FOREIGN KEY (company_id) REFERENCES companies(id)
);

products (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  sku VARCHAR(100) UNIQUE,
  price DECIMAL(10,2),
  product_type VARCHAR(50)
);

inventory (
  id INT PRIMARY KEY,
  product_id INT,
  warehouse_id INT,
  quantity INT,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
  UNIQUE (product_id, warehouse_id)
);

inventory_changes (
  id INT PRIMARY KEY,
  inventory_id INT,
  change_amount INT,
  reason VARCHAR(100),
  created_at TIMESTAMP
);

suppliers (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  contact_email VARCHAR(255)
);

product_suppliers (
  product_id INT,
  supplier_id INT,
  PRIMARY KEY (product_id, supplier_id)
);

product_bundles (
  bundle_id INT,
  child_product_id INT,
  quantity INT
);
