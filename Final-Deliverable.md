# Multi-Vendor Artisan E-Commerce Marketplace

## 1. Problem Statement

The system is an online marketplace that enables independent craftspeople to set up storefronts, manage product catalogs, receive orders, and receive automated split payouts with platform commission deductions.

---

## 2. Requirements

### 2.1 Functional Requirements

<table>
<thead>
<tr>
<th>ID</th>
<th>Type</th>
<th>Description</th>
<th>Priority</th>
<th>Acceptance Criteria</th>
<th>Rationale</th>
</tr>
</thead>
<tbody>

<tr>
<td>FR-001</td>
<td>Functional</td>
<td>The system shall allow Artisan Vendors to create and manage their storefronts and product catalogs, including adding, updating, and removing product listings.</td>
<td>High</td>
<td>Pass: An Artisan Vendor can create a storefront and successfully add, update, or remove their product listings. Fail: The vendor cannot perform one or more of these operations.</td>
<td>Artisan Vendors need to maintain their storefronts and keep product information accurate and up to date.</td>
</tr>

<tr>
<td>FR-002</td>
<td>Functional</td>
<td>The system shall allow Shoppers to browse and search products offered by multiple Artisan Vendors.</td>
<td>High</td>
<td>Pass: A Shopper can browse available products and search for products using relevant search criteria. Fail: The Shopper cannot find or view available products.</td>
<td>Shoppers need to discover products from different Artisan Vendors on the marketplace.</td>
</tr>

<tr>
<td>FR-003</td>
<td>Functional</td>
<td>The system shall allow Shoppers to add products from one or more Artisan Vendors to a cart and proceed to checkout.</td>
<td>High</td>
<td>Pass: A Shopper can add available products from multiple vendors to the cart and proceed to checkout with the selected items. Fail: Products cannot be added or the Shopper cannot proceed to checkout.</td>
<td>The marketplace must support purchases involving products from multiple independent vendors.</td>
</tr>

<tr>
<td>FR-004</td>
<td>Functional</td>
<td>The system shall process customer cart payments by splitting the payment among the respective Artisan Vendors and deducting a 5% platform commission.</td>
<td>High</td>
<td>Pass: The total split payouts plus the 5% platform commission equal the customer's cart payment amount. Fail: The calculated payouts do not balance with the cart payment.</td>
<td>Automated split payouts are a core feature of the multi-vendor marketplace.</td>
</tr>

<tr>
<td>FR-005</td>
<td>Functional</td>
<td>The system shall allow Artisan Vendors to view orders containing their products and manage the status of those orders.</td>
<td>High</td>
<td>Pass: An Artisan Vendor can view their received orders and update the status of an order. Fail: The vendor cannot view or update their relevant orders.</td>
<td>Vendors need to receive and manage orders for products purchased by Shoppers.</td>
</tr>

</tbody>
</table>

### 2.2 Non-Functional Requirements

<table>
<thead>
<tr>
<th>ID</th>
<th>Type</th>
<th>Description</th>
<th>Priority</th>
<th>Acceptance Criteria</th>
<th>Rationale</th>
</tr>
</thead>
<tbody>

<tr>
<td>NFR-001</td>
<td>Performance</td>
<td>The product catalog shall support high-resolution image rendering with CDN caching and achieve product catalog load times of less than 500 ms under the defined test conditions.</td>
<td>High</td>
<td>Pass: Benchmarking confirms that the required catalog requests achieve a load time below 500 ms under simulated peak load. Fail: The target load time is not achieved.</td>
<td>Fast product loading provides a responsive shopping experience, especially when displaying high-resolution artisan product images.</td>
</tr>

<tr>
<td>NFR-002</td>
<td>Security</td>
<td>The system shall securely authenticate Shoppers and Artisan Vendors and protect payment, account, storefront, and order information from unauthorized access.</td>
<td>High</td>
<td>Pass: Only authenticated and authorized users can access protected information and perform permitted operations. Fail: Unauthorized users can access protected information or perform restricted operations.</td>
<td>The marketplace handles customer accounts, vendor information, orders, and payment-related data that require protection.</td>
</tr>

</tbody>
</table>

---

## 3. UML Use-Case Diagram

![Use-Case Diagram](UML/Use-Case-Diagram.drawio.png)

### 3.1 Actors

#### Shopper

The Shopper browses and searches products, adds products to the cart, places orders, and processes payments.

#### Artisan Vendor

The Artisan Vendor manages the storefront and product catalog, views orders, and updates order status.

### 3.2 Use Cases

#### Shopper Use Cases

- Browse Products
- Search Products
- Apply Filters
- Add Products to Cart
- Place Order
- Process Payment
- Split Payment
- Deduct 5% Platform Commission

#### Artisan Vendor Use Cases

- Manage Storefront
- Manage Product Catalog
- View Orders
- Update Order Status

### 3.3 UML Relationships

- `Place Order` includes `Process Payment`.
- `Process Payment` includes `Split Payment`.
- `Split Payment` includes `Deduct 5% Platform Commission`.
- `Apply Filters` extends `Search Products`.

---

## 4. Use Case Flow — Split Payment

### Use Case ID

UC-01

### Use Case Name

Split Payment

### Primary Actor

Shopper

### Supporting Actor

Artisan Vendor

### Preconditions

1. The Shopper has selected products from one or more Artisan Vendors.
2. The selected products have been added to the Shopper's cart.
3. The Shopper has proceeded to checkout.
4. The total cart payment amount has been calculated.
5. The payment information provided by the Shopper is valid.

### Main Success Scenario

1. The Shopper proceeds to checkout.
2. The system calculates the total amount of the Shopper's cart.
3. The system identifies the Artisan Vendor associated with each product in the order.
4. The system processes the Shopper's payment.
5. The system calculates the 5% platform commission.
6. The system deducts the 5% platform commission from the total payment.
7. The system calculates the amount payable to each Artisan Vendor.
8. The system splits the remaining payment among the respective Artisan Vendors.
9. The system verifies that the vendor payouts and the platform commission equal the original payment amount.
10. The system records the successful payment and corresponding vendor payouts.
11. The system confirms successful payment to the Shopper.

### Alternate Flows

#### A1. Payment Failure

1. The system attempts to process the payment.
2. The payment fails.
3. The system does not create vendor payouts.
4. The system informs the Shopper that the payment was unsuccessful.
5. The Shopper may retry the payment.

#### A2. Invalid Payment Split

1. The system calculates the vendor payouts and platform commission.
2. The system detects that the calculated amounts do not equal the original payment amount.
3. The system does not complete the payout.
4. The system records the payment split error.
5. The system informs the appropriate administrator or displays an error message.

#### A3. Multiple Artisan Vendors

1. The system identifies multiple Artisan Vendors in the Shopper's order.
2. The system calculates the amount attributable to each Artisan Vendor.
3. The system calculates and deducts the 5% platform commission.
4. The system distributes the remaining payment among the respective Artisan Vendors.
5. The system verifies that the total payouts and commission equal the original payment amount.

### Postconditions

1. The Shopper's payment is successfully recorded.
2. The 5% platform commission is recorded.
3. The appropriate payout amount is calculated for each Artisan Vendor.
4. The split payouts are recorded for the respective Artisan Vendors.
5. The order is marked as successfully paid.