# Portfolio-project-5
Portfolio Project 5 - E-commerce Applications

# 📝 InkWell – A Premium Blogging Platform

**InkWell** is a full-stack blogging platform that allows authors to publish both public and subscriber-only posts. It includes e-commerce integration for subscriptions, secure role-based authentication, SEO features, and a clean, accessible UI.

## 📌 Table of Contents
- [Project Overview](#project-overview)
- [User Types & User Stories](#user-types--user-stories)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Agile Workflow](#agile-workflow)
- [Wireframes & UX Design](#wireframes--ux-design)
- [Setup Instructions](#setup-instructions)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)

## How to View the Project
- [View the deployed website on Heroku](https://inkwell-blog-8edefa7bcffe.herokuapp.com/)
- [View the website repository on GitHub](https://github.com/AlexeyKopchinskiy/Portfolio-project-5-v2)

## 📖 Project Overview

This platform allows authors to manage and monetize content while providing a premium experience for paid subscribers. The goal is to provide a clean, SEO-optimized, and secure blogging space with real e-commerce functionality.

## 👥 User Types & User Stories

### Site Owner
- Manage posts, categories, and publishing schedule
- Track subscribers and view platform analytics
- Receive notifications of new subscriptions and comments

### Visitor / Reader
- Browse and read public blog posts without registration
- Register, log in, and subscribe for premium content
- Like, bookmark, and comment on posts

Check out the full list of [user stories and issues here](#) ← *(you can link to your Issues tab or GitHub project board)*

## ✨ Features

- Stripe-powered subscriptions
- Public and premium post access
- Role-based authentication
- Responsive, accessible UI with dark/light mode
- Bookmarking, commenting, and category filters
- Facebook product page / promotional mockup
- Newsletter signup and SEO features (meta tags, sitemap)
- Functional contact form

### 📮 Contact Form Feature

The application includes a fully functional contact form accessible via /contact/. Visitors can submit their name, email, subject, and message directly through the form.

- Submissions are stored in the database via the custom ContactMessage model.
- Messages are timestamped and can be browsed via the Django admin interface.
- User feedback is provided after successful form submission.
- The form is styled with Bootstrap 5 for responsive and accessible design.
- CSRF protection and validation are included.

**This feature demonstrates:**

- Form handling with validation (LO1.4)
- Creation of a custom Django model (LO1.12)
- Clean code with Bootstrap styling and UX considerations (LO2.1)

## 🛠 Technologies & Software Used

| Purpose            | Tool(s)                       |
|--------------------|-------------------------------|
| Code Development   | Visual Studio Code            |
| Backend Framework  | Django (Python)               |
| Database           | PostgreSQL                    |
| DB modelling       | Dbdiagram.io                  |
| UI Styling         | HTML, CSS, Bootstrap          |
| Design/Mockups     | CorelDraw, Photoshop          |
| Wireframing        | CorelDraw, Photoshop          |
| Deployment         | Heroku (or similar)           |
| Payments           | Stripe API                    |
| Version Control    | Git & GitHub                  |
| Github emoji       | Github emoji markup           |

## 🚀 Agile Workflow

- Agile board managed with GitHub Issues and Milestones  
- User stories split into:
  - Developer stories
  - Site owner stories
  - Visitor stories
- Labels include `Must-Have`, `Should-Have`, and `Could-Have`
- Milestones:
  - Project Setup
  - Auth & Roles
  - E-Commerce
  - Blog Engine
  - UX/UI
  - SEO & Marketing
  - Testing & Deployment

## 📐 Wireframes & UX Design

- Homepage  
- Post detail & premium prompt  
- Admin dashboard  
- User profile | saved posts  

### Website low-fidelity wireframes

#### 🏠 Homepage (Public View)

![Homepage wireframe](./static/img/pp5-wireframe-startpage.png)

#### Mobile Homepage

![Homepage wireframe mobile](./static/img/pp5-wireframe-mobile-homepage-simple.png)

#### Mobile Blog Post Details

![Blog post detaile mobile view](./static/img/pp5-wireframe-mobile-blog-post-details-simple.png)

### Mobile Login/register page

![Mobile login / register page](./static/img/pp5-wireframe-mobile-login-register-page.png)

### Mobile Member Page

![Mobile Member Page](./static/img/pp5-wireframe-mobile-member-page.png)

## 🔧 Django Apps

| **App name**    | **Purpose**                                  |
|-----------------|----------------------------------------------|
| blog            | Posts, categories, tags, post detail views   |
| accounts        | Custom user model, login, registration       |
| subscriptions   | Stripe integration, premium access control   |
| core            | Homepage, about, footer, reusable templates  |
| admin_dashboard | Admin-only views for content and analytics   |

## DB Modelling

**dbdiagram.io** is used for DB modelling

### 👦 User model
```
Table users {
  id integer [primary key]
  username varchar
  role varchar
  created_at timestamp
}
```

### 📃 Posts model
```
Table posts {
  id integer [primary key]
  title varchar
  body text [note: 'Content of the post']
  user_id integer [not null]
  status varchar
  created_at timestamp
}
```

### 🐾 Following users
```
Table follows {
  following_user_id integer
  followed_user_id integer
  created_at timestamp
}
```

### 🏷️ tags (many-to-many with posts)
```
Table tags {
  id integer [primary key]
  name varchar
  slug varchar
}

Table post_tags {
  post_id integer [ref: > posts.id]
  tag_id integer [ref: > tags.id]
}
```

### 💬 Comments or discussion
```
Table comments {
  id integer [primary key]
  post_id integer [ref: > posts.id]
  user_id integer [ref: > users.id]
  content text
  created_at timestamp
}
```

### 💼 Premium subscriptions (tied to Stripe IDs)
```
Table subscriptions {
  id integer [primary key]
  user_id integer [ref: > users.id]
  plan varchar
  started_on timestamp
  expires_on timestamp
  stripe_customer_id varchar
}
```

## SQL markdown

![SQL markdown](./static/img/sql-markdown.png)

## User access rights

| View / action                  |   Groups allowed      |     Description    |
|--------------------------------|-----------------------|--------------------|
| Admin Dashboard (/admin/)      | Admins (via is_staff) | Full access to Django's built-in admin site for managing models, users, and site data.                   |
| Author Dashboard (/dashboard/) | Authors, Editors      | Personal workspace to manage drafts, edit posts, view writing stats. |
| Create New Post                | Authors               | Access to a post creation form and the ability to submit content for review or publication. |
| Edit/Delete Own Post           | Authors               | Authors can update or remove only the posts they’ve authored. |
| Edit/Publish Any Post          | Editors, Admins       | Editors and admins can modify or publish any post on the platform, not just their own. |
| View Published Posts           | Everyone              | Public blog posts are viewable by anyone visiting the site. |
| Comment on Posts               | Logged-in Users       | Users with accounts can write comments on posts. |
| Moderate/Delete Comments       | Moderators, Editors, Admins | Ability to remove or flag inappropriate comments and maintain community standards |
| Manage User Groups / Permissions | Admins (via Django admin) | Only superusers can assign groups, roles, and advanced permissions via the admin panel. |
| View Subscription Settings     | Logged-in Users (Readers, Authors) | Access to personal subscription status, invoices, and upgrade/cancel options. |
| Access Premium Content         | Anyone with is_premium=True | Restricts access to exclusive or paywalled content for premium subscribers only. |

## ⚙️ Setup Instructions

```bash
git clone https://github.com/your-username/inkwell.git
cd inkwell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## ✅ Testing
- Manual testing checklist available in the /testing folder
- Unit and integration tests written using Django’s TestCase framework
- Accessibility and SEO audited with Lighthouse

## 🚢 Deployment
- Live app hosted on Heroku (or insert platform)
- Environment variables managed securely via .env files
- DEBUG = False and secret keys hidden in production

## 📄 License
🧑‍💻 Code
This project is licensed under the dual-license (MIT License + Creative Commons).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✍️ Content
All original written content (blog posts, mock posts, text) is licensed under
Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

## 🙌 Acknowledgements
Special thanks to the tutors, the assessment handbook, and caffeine.