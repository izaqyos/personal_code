# Pomodoro Timer App

A simple and effective Pomodoro Timer application built with React and TypeScript.

## What is the Pomodoro Technique?

The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks. Each interval is known as a pomodoro, from the Italian word for tomato, after the tomato-shaped kitchen timer Cirillo used as a university student.

## Features

- 25-minute work sessions (pomodoros)
- 5-minute short breaks
- 15-minute long breaks after 4 pomodoros
- Timer controls (start, pause, reset)
- Session type selector
- Pomodoro counter
- Audio notification when timer completes

## Getting Started

### Prerequisites

- Node.js (12.x or higher)
- npm or yarn

### Installation

1. Clone the repository or download the source code
2. Navigate to the project directory
3. Install dependencies:

```bash
npm install
# or
yarn install
```

### Running the App

```bash
npm start
# or
yarn start
```

This will start the development server and open the app in your browser at `http://localhost:3000`.

### Building for Production

```bash
npm run build
# or
yarn build
```

## Running Tests

```bash
npm test
# or
yarn test
```

## Project Structure

```
src/
  ├── components/
  │   ├── Controls.tsx        # Timer control buttons
  │   ├── ModeSelector.tsx    # Work/break mode selector
  │   ├── PomodoroApp.tsx     # Main app component
  │   ├── PomodoroApp.css     # App styling
  │   └── Timer.tsx           # Timer display component
  │
  ├── App.tsx                 # Root app component
  ├── App.css                 # Root app styling
  ├── index.tsx               # Entry point
  └── ...
```

## License

MIT
