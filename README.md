# 💎 GoldenAura 960 | Premium E-Commerce Platform

GoldenAura 960 is an end-to-end, full-stack luxury e-commerce web application crafted with Python, Django, and Bootstrap 5. Designed specifically for high-end jewellery retail, it offers a seamless shopping experience through a custom-styled **Mocha, Champagne Gold, and Burnt Amber** UI palette, complete order lifecycle management, and secure multi-tier payment gateways.

---

## 📖 About The Project

GoldenAura 960 bridges the gap between traditional luxury boutique shopping and modern digital convenience. Built with scalability and security at its core, the platform provides clients with bespoke jewellery customization, instant delivery tracking, real-time invoice generation, and an intuitive customer service concierge interface.

The application adheres to production-grade architecture standards, complete with dynamic database models, granular role-based access control, transaction-safe database operations, and defensive security measures.

---

## ✨ Key Technical Features

### 🔐 1. Authentication & Security
- **OTP-Based Forgot Password Workflow**: Secure multi-step password resetting via email/OTP verification.
- **Role-Based Access**: Dedicated client dashboard, administrative portal, and secure session management.

### 🛍️ 2. Core E-Commerce & Product Discovery
- **Flexible Sizing & Ring Fitting**: Interactive size selector tailored for rings, bangles, and custom metal variants.
- **Dynamic Wishlist System**: Instant wishlist toggling for logged-in clients.
- **Smart Cart Management**: Real-time total estimation, item quantity modifiers, and persistent user carts.
- **Verified Customer Review & Rating System**: Real-time client feedback and rating widgets on product detail pages.

### 💳 3. Checkout, Billing & Payment Gateways
- **Modern Express Checkout**: Clean multi-step checkout form pre-filling verified client details.
- **Dual Payment Architecture**:
  - **Razorpay Integration**: Seamless online payment workflow using Webhooks and Razorpay Test Mode.
  - **Cash on Delivery (COD)**: Automated cash-on-delivery order placement pipeline.
- **Dynamic PDF Billing & Invoice System**: Automatic tax-compliant PDF invoice creation for downloadable order records.

### 📦 4. Order Lifecycle, Returns & Cancellation
- **48-Hour Order Cancellation**: Smart cancellation engine allowing users to cancel orders in "Pending" or "Processing" states within a 48-hour window directly from the dashboard.
- **Comprehensive Return Policy & Refund Tracking**: Automated return requests for delivered orders with multi-state refund processing (`Pending` → `Approved` → `Refund Details Input` → `Completed`).
- **Interactive Delivery Tracking**: Modal-based logistics transit tracking.

### 💬 5. Client Support & Concierge Service
- **Dedicated Assistant Support**: Integrated 24/7 client support modal for hallmark certificates, insured shipments, and custom resizing queries.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | Python 3.14+, Django 6.1+ |
| **Frontend UI** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Font Awesome 6, Google Fonts (*Cinzel & Plus Jakarta Sans*) |
| **Database** | SQLite3 (Development) / PostgreSQL-ready |
| **Payment Gateways** | Razorpay Payment API |
| **Version Control** | Git & GitHub |

---

## 📂 Project Architecture