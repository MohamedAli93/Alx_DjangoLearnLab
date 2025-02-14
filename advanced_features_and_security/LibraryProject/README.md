# Django Permissions & Groups Implementation

## Overview
This project implements **permissions and groups** in Django.

### Features:
- **Custom Permissions** (`can_view`, `can_create`, `can_edit`, `can_delete`)
- **User Groups**:
  - `Viewers`: Can only view books.
  - `Editors`: Can view, create, and edit books.
  - `Admins`: Can view, create, edit, and delete books.

## How to Use
1. **Run Migrations**:
2. **Create Users in Django Admin** (`/admin`).
3. **Assign Users to Groups** (`Viewers`, `Editors`, `Admins`).
4. **Test Access Control**:
- Login with different users.
- Verify restricted access to **create, edit, delete** books.

---