import "./App.css";

import { createContext, useContext, useState, useEffect } from "react";
import Home from "./routes/Home";
import CssBaseline from "@mui/material/CssBaseline";
import About from "./routes/About";
import Blog from "./routes/Blog";
import ErrorPage from "./routes/ErrorPage";
import { createTheme, ThemeProvider } from "@mui/material/styles";

import { createHashRouter, RouterProvider } from "react-router-dom";
export const DarkThemeContext = createContext();

export const DarkThemeProvider = ({ children, value }) => {
  return (
    <DarkThemeContext.Provider value={value}>
      {children}
    </DarkThemeContext.Provider>
  );
};

export const useTheme = () => {
  return useContext(DarkThemeContext);
};
const router = createHashRouter([
  {
    path: "/",
    element: <Home />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/home",
    element: <Home />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/blog",
    element: <Blog />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/about",
    element: <About />,
    errorElement: <ErrorPage />,
  },
]);

const App = (props) => {
  const { isDarkMode } = props;
  const [isDarkTheme, setIsDarkTheme] = useState(isDarkMode);
  const setTheme = (isDarkTheme) =>
    createTheme({
      palette: {
        mode: isDarkTheme ? "dark" : "light",
      },
    });
  useEffect(() => {});

  const toggleTheme = () => {
    setIsDarkTheme((isDarkTheme) => !isDarkTheme);
  };

  return (
    <DarkThemeProvider value={{ isDarkTheme, toggleTheme }}>
      <ThemeProvider theme={setTheme(isDarkTheme)}>
        <CssBaseline />
        <RouterProvider router={router} />
      </ThemeProvider>
    </DarkThemeProvider>
  );
};

export default App;
