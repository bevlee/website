import * as React from "react";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Markdown from "../Components/Markdown";
import Container from "@mui/material/Container";
import Footer from "../Components/Footer";
import Header from "../Components/Header";
import blog1 from "../blogs/The_Beginning.md";
import blog2 from "../blogs/Running_10km.md";

function Blog(props) {
  const [blogs, setBlogs] = useState([]);
  useEffect(() => {
    const blogTitles = [blog1, blog2];
    const getBlogs = async () => {
      const res = await Promise.all(
        blogTitles.map(async (src) => {
          const response = await fetch(src);
          const text = await response.text();
          console.log(text);
          return text;
        })
      );
      setBlogs(res);
    };
    getBlogs();
  }, []);

  return (
    <>
      <Container maxWidth="lg">
        <Header title="Bevsoft" />
        <Grid
          item
          xs={12}
          md={8}
          sx={{
            "& .markdown": {
              py: 3,
            },
          }}
        >
          <Typography variant="h6" gutterBottom>
            {"Blogs"}
          </Typography>
          <Divider />
          {blogs.map((post) => (
            <Markdown className="markdown" key={post.substring(0, 40)}>
              {post}
            </Markdown>
          ))}
        </Grid>
      </Container>
      <Footer />
    </>
  );
}

Blog.propTypes = {
  posts: PropTypes.arrayOf(PropTypes.string).isRequired,
  title: PropTypes.string.isRequired,
};

export default Blog;
