import { useRouteError } from "react-router-dom";

import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Header from "../Components/Header";
import Footer from "../Components/Footer";

export default function ErrorPage() {
  const error = useRouteError();
  return (
    <>
      <Container maxWidth="lg">
        <Header title="Bevsoft" />
        <Paper elevation={0} sx={{ p: 2, bgcolor: "grey.200" }}>
          <Typography variant="h6" gutterBottom>
            {"hello"}
          </Typography>
          <Typography>
            <div id="error-page">
              <h1>Oops!</h1>
              <p>Sorry, an unexpected error has occurred.</p>
              <p>
                <i>{error.statusText || error.message}</i>
              </p>
            </div>
          </Typography>
        </Paper>
        <main></main>
      </Container>
      <Footer />
    </>
  );
}
