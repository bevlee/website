import * as React from "react";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Header from "../Components/Header";
import Footer from "../Components/Footer";

export default function About() {
  return (
    <>
      <Container maxWidth="lg">
        <Header title="Bevsoft" />
        <Paper elevation={0} sx={{ p: 2, bgcolor: "grey.600" }}>
          <Typography variant="h6" gutterBottom>
            {"ABOUT ME"}
          </Typography>
          <Typography>
            <div>
              Hi my name is Bevan. My current focuses are
              <ul>
                <li>Learning </li>
                <li>Music</li>
                <li>Web dev</li>
              </ul>
            </div>
          </Typography>
        </Paper>
        <main></main>
      </Container>
      <Footer />
    </>
  );
}
