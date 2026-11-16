# IMDB Movies – Vue Application

A movie management application built using **Vue 3, TypeScript, Pinia, Vuetify and Vite**. The application allows users to explore, create, edit and delete movies, manage movie-related information, and upload movie posters.

## Features

- **Movie Listing:** View all movies in a responsive card-based layout.
- **Explore Movies:** View detailed information about individual movies.
- **Create Movies:** Add new movies with relevant information.
- **Edit Movies:** Fetch existing movie details from the API and prefill the form.
- **Delete Movies:** Delete movies with confirmation.
- **Poster Upload:** Upload movie posters separately.
- **People Management:** Manage actors and producers.
- **Genre Management:** Retrieve and associate genres with movies.
- **Authentication:** Initialize authentication and manage API authorization.
- **Responsive UI:** Built using Vuetify components and layouts.

## Technology Stack

| Technology | Purpose |
|---|---|
| Vue 3 | Frontend framework |
| TypeScript | Static typing |
| Vite | Development server and build tool |
| Pinia | State management |
| Vue Router | Client-side routing |
| Vuetify | UI component framework |
| Axios | HTTP communication |
| SweetAlert2 | Confirmation and alert dialogs |

## Project Structure

```text
client/
├── public/
├── src/
│   ├── assets/
│   │   ├── images/
│   │   └── main.css
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   └── AppNavbar.vue
│   │   ├── movies/
│   │   │   ├── MovieCard.vue
│   │   │   └── MovieDetailModal.vue
│   │   └── shared/
│   │       ├── LoadingMovies.vue
│   │       ├── LoadingSpinner.vue
│   │       └── PersonFormDialog.vue
│   │
│   ├── views/
│   │   ├── Movies.vue
│   │   ├── MovieForm.vue
│   │   └── NotFound.vue
│   │
│   ├── stores/
│   │   ├── index.ts
│   │   └── modules/
│   │       ├── movie.ts
│   │       ├── actor.ts
│   │       ├── producer.ts
│   │       └── genre.ts
│   │
│   ├── services/
│   │   ├── index.ts
│   │   └── modules/
│   │       ├── api.ts
│   │       ├── movieService.ts
│   │       ├── actorService.ts
│   │       ├── producerService.ts
│   │       ├── genreService.ts
│   │       ├── authService.ts
│   │       └── authToken.ts
│   │
│   ├── types/
│   │   ├── index.ts
│   │   └── modules/
│   │       ├── api.ts
│   │       ├── movie.ts
│   │       ├── person.ts
│   │       └── genre.ts
│   │
│   ├── router/
│   │   └── index.ts
│   │
│   ├── plugins/
│   │   └── vuetify.ts
│   │
│   ├── App.vue
│   └── main.ts
│
├── index.html
├── package.json
├── package-lock.json
└── vite.config.ts
```

## Application Architecture

The application follows a modular structure with separate responsibilities for UI, state management and API communication.

```text
Views / Components
        |
        v
   Pinia Stores
        |
        v
   API Services
        |
        v
    API Layer
        |
        v
    Backend API
        |
        v
      Database
```

- **Views:** Handle application pages and coordinate components.
- **Components:** Provide reusable UI elements.
- **Stores:** Manage shared application state using Pinia.
- **Services:** Contain API-related operations.
- **API Layer:** Handles HTTP requests, responses and errors.
- **Types:** Define TypeScript interfaces and data structures.
- **Router:** Manages application navigation.

## Application Routes

| Route | Description |
|---|---|
| `/` | Redirects to movies |
| `/movies` | Movie listing page |
| `/movies/create` | Create a new movie |
| `/movies/:id/edit` | Edit an existing movie |
| `/:pathMatch(.*)*` | Not Found page |

## Installation and Setup

### Prerequisites

- Node.js
- npm
- Running backend API

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the client directory

```bash
cd client
```

### 3. Install dependencies

```bash
npm install
```

### 4. Configure environment variables

Create a `.env` file in the client directory:

```env
VITE_API_BASE_URL=<your-backend-api-url>
```

Replace the placeholder with your backend API base URL.

### 5. Start the development server

```bash
npm run dev
```

The application will be available at the local URL provided by Vite, usually:

```text
http://localhost:5173
```

## Available Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start development server |
| `npm run build` | Build production application |
| `npm run preview` | Preview production build |
| `npm run type-check` | Run TypeScript checks |
| `npm run lint` | Check code quality |
| `npm run format` | Format source files |

## Backend Integration

The frontend communicates with the backend through a centralized API layer.

The API services are organized by resource:

- Movie Service
- Actor Service
- Producer Service
- Genre Service
- Authentication Service

This separation keeps HTTP communication independent from UI components and makes the application easier to maintain.

## Build for Production

```bash
npm run build
```

The production-ready files are generated inside the `dist/` directory.

These files can be deployed to static hosting platforms such as Netlify.

