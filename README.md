# EventHub — Event Management & Ticket Booking System (EMTBS)
*Built in strict adherence to IEEE Std 830-1998 Software Requirements Specification*

---

## 🌟 Overview & UI Match

EventHub is a modern, high-performance web application designed for organizing, discovering, and booking events with atomic concurrency inventory controls and verified QR digital tickets.

The frontend user interface is built to replicate the dark violet/neon aesthetic:
- **Hero Section:** Ambient concert background, signature typography: *"Your Next Unforgettable Event Awaits!"*, integrated pill search bar with keyword search, location dropdown (`All Locations`, `Kochi`, `Mumbai`, `Goa`, `Trivandrum`, `Bengaluru`, `Delhi NCR`, `Hyderabad`), and glowing purple Search button.
- **Category Pill Bar:** Filter tabs with icons for *Concerts*, *Shows & Theatre*, *Sports*, *Conferences*, *Festivals*, *Events & Gaming*, and *Workshops*.
- **Popular Events:** High-resolution card grid matching the UI mockup:
  - 🎤 **The Weeknd Live in Concert** (Kochi) — ₹2,999 onwards
  - 🏏 **India vs Australia – T20** (Mumbai) — ₹1,499 onwards
  - 🏖️ **Sunburn Music Festival** (Goa) — ₹3,499 onwards
  - 🤖 **AI & Innovation Workshop** (Trivandrum) — ₹999 onwards

---

## 🚀 Live Servers Running

Both the frontend and backend servers are running live on your system:
- **Frontend App:** [http://localhost:5173](http://localhost:5173) or [http://127.0.0.1:5173](http://127.0.0.1:5173)
- **Django REST API:** [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)
- **Django Admin Console:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Pre-Seeded Demo Accounts (1-Click Login Supported)

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Attendee** | `attendee@eventhub.com` | `Attendee@123` | Browse, book tickets, view QR passes, cancel & refund |
| **Organizer** | `organizer@eventhub.com` | `Organizer@123` | Publish events, create ticket tiers, view sales, export CSV, QR admission scanner |
| **Admin** | `admin@eventhub.com` | `Admin@123` | Platform oversight, activate/deactivate users, change roles, revenue analytics |

---

## 🛠️ Technology Stack (SRS Section 7)

### **Frontend**
- **Framework:** React 18 (Functional components & hooks) built with **Vite 5**
- **Routing:** React Router v6
- **Styling:** Tailwind CSS (Custom dark theme with `#0a0915` palette & glow shadows)
- **Icons:** Lucide React
- **Visuals & Effects:** canvas-confetti, CSS glassmorphism

### **Backend**
- **Framework:** Python 3.12, Django 6.1, Django REST Framework 3.18
- **Authentication:** `djangorestframework-simplejwt` (JWT Access & Refresh tokens)
- **Concurrency & Database:** Atomic transactions with `select_for_update()` row-level locking
- **E-Ticket Generation:** ReportLab (PDF) & Python `qrcode` (Base64 data URIs)
- **CORS:** `django-cors-headers`

---

## 📑 Requirements Traceability (SRS Checklist)

| SRS Requirement | Implementation Detail | Status |
|---|---|:---:|
| **FR-AUTH-01 to 04** | Email & password auth with JWT, 8+ char mixed-case password rule enforcement | ✅ Completed |
| **FR-EVT-01 to 06** | Search by keyword, filters (category, city, dates), sorting (date, price, popularity) | ✅ Completed |
| **FR-BKG-01 to 03** | Max 10 tickets per booking, real-time availability check, 10-minute hold timer | ✅ Completed |
| **FR-BKG-04 to 06** | Subtotal, GST taxes, service fee, promo codes (`WELCOME50`, `EVENTHUB10`), row-level concurrency lock | ✅ Completed |
| **FR-BKG-07 to 08** | Digital e-ticket issuance with scannable QR code & confirmation log | ✅ Completed |
| **FR-MBK-01 to 05** | My Bookings, PDF e-ticket download via ReportLab, 48h cancellation & refund policy | ✅ Completed |
| **FR-ORG-01 to 05** | Organizer event creation, multi-tier tickets, attendee roster, CSV export, gate QR validator | ✅ Completed |
| **FR-ADM-01 to 04** | Platform analytics (revenue, bookings, top events), user management & role switching | ✅ Completed |
| **NFR-11** | Automated test suite (11 test cases in `users/tests.py`, `events/tests.py`, `bookings/tests.py`) | ✅ 100% Passing |

---

## 🧪 Running Automated Tests

To run the backend test suite:
```bash
python manage.py test
```
All 11 tests pass with:
```
Ran 11 tests in 17.947s
OK
```

---

## 🖥️ Standalone Launch Scripts

If you close the current session, you can relaunch anytime using the provided batch files:
- **`run_all.bat`** — Launches both backend and frontend servers in separate windows.
- **`run_backend.bat`** — Starts Django backend on `http://127.0.0.1:8000`
- **`run_frontend.bat`** — Starts Vite frontend on `http://localhost:5173`
