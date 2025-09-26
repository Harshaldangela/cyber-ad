# SMS Spam Classifier React UI

This is a React-based user interface for the SMS Spam Classifier project. It provides a modern, responsive web application with enhanced features compared to the original Streamlit version.

## Features

- **Modern React UI**: Built with React.js and styled-components for a responsive, component-based architecture
- **Dark/Light Mode**: Toggle between themes based on user preference
- **Analytics Dashboard**: Visualize spam detection statistics with interactive charts
- **Classification History**: Track and review previous classifications
- **Cyber Awareness Ads**: Generate educational content for detected spam messages
- **Multi-language Support**: Translate awareness content to multiple languages
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Project Structure

```
react-ui/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   ├── Classifier.js
│   │   ├── Analytics.js
│   │   ├── History.js
│   │   └── About.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Prerequisites

- Node.js (version 14 or higher)
- npm (usually comes with Node.js)

## Installation

1. Navigate to the react-ui directory:
   ```bash
   cd react-ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm start
   ```

2. Open your browser and visit `http://localhost:3000`

## Building for Production

To create a production build:
```bash
npm run build
```

## Dependencies

- React.js
- React Router DOM
- Styled Components
- Axios
- Chart.js
- React Chartjs 2
- React Icons

## Integration with Backend

This React UI is designed to work with the Python backend API. To connect:

1. Ensure the Python API is running on `http://localhost:8000`
2. Enter your Gemini API key in the header input field
3. The application will automatically communicate with the backend for:
   - Message classification
   - Cyber awareness ad generation
   - Ad translation

## Customization

### Theme
The application supports both light and dark themes. Users can toggle between themes using the button in the header.

### Styling
All styling is done with styled-components, making it easy to customize the look and feel.

### Components
Each major section of the application is built as a separate component, making it easy to modify or extend functionality.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.