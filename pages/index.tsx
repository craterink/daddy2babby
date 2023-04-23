import React, { useState } from "react";
import Link from "next/link";
import { styled } from "@mui/material/styles";
import LinearProgress, {
  linearProgressClasses,
} from "@mui/material/LinearProgress";
import { Box } from "@mui/material";
import { DefinePage } from "../components/define";

const pages = ["define", "examples", "distill", "playground"];
const pageTitles = {
  define: "Define task",
  examples: "Build examples",
  distill: "Distill model",
  playground: "Playground",
};

const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
  height: 10,
  borderRadius: 5,
  [`&.${linearProgressClasses.colorPrimary}`]: {
    backgroundColor:
      theme.palette.grey[theme.palette.mode === "light" ? 200 : 800],
  },
  [`& .${linearProgressClasses.bar}`]: {
    borderRadius: 5,
    backgroundColor: theme.palette.mode === "light" ? "#1a90ff" : "#308fe8",
  },
}));

const HomePage = () => {
  const [currentPage, setCurrentPage] = useState("define");
  const nextPage = pages[pages.indexOf(currentPage) + 1];

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <div>
      <Navigation currentPage={currentPage} />
      <PageContent
        currentPage={currentPage}
        handlePageChange={handlePageChange}
      />
      {currentPage != "playground" && (
        <NextPageButton
          nextPage={nextPage}
          handlePageChange={handlePageChange}
        />
      )}
    </div>
  );
};

export default HomePage;

const Navigation = ({ currentPage }: { currentPage: string }) => {
  const progress = (pages.indexOf(currentPage) / (pages.length - 1)) * 100;

  return (
    <div>
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          marginTop: "32px",
        }}
      >
        <BorderLinearProgress
          variant="determinate"
          value={progress}
          sx={{ width: "75%" }}
        />
      </Box>
      <Box
        sx={{
          position: "relative",
          display: "flex",
          flexDirection: "row",
          paddingTop: "8px",
        }}
      >
        {pages.map((page, index) => (
          <Box
            key={page}
            sx={{
              width: "25%",
              textAlign: "center",
            }}
          >
            {pageTitles[page]}
          </Box>
        ))}
      </Box>
    </div>
  );
};

const PageContent = ({
  currentPage,
  handlePageChange,
}: {
  currentPage: string;
  handlePageChange: any;
}) => {
  switch (currentPage) {
    case "define":
      return <DefinePage handlePageChange={handlePageChange} />;
    case "examples":
      return <ExamplesPage handlePageChange={handlePageChange} />;
    case "distill":
      return <DistillPage handlePageChange={handlePageChange} />;
    case "playground":
      return <PlaygroundPage handlePageChange={handlePageChange} />;
    default:
      return <DefinePage handlePageChange={handlePageChange} />;
  }
};

const ExamplesPage = ({ handlePageChange }) => {
  return (
    <div>
      <h2>Examples Page</h2>
      <p>This is the examples page content.</p>
    </div>
  );
};

const DistillPage = ({ handlePageChange }) => {
  return (
    <div>
      <h2>Distill Page</h2>
      <p>This is the distill page content.</p>
    </div>
  );
};

const PlaygroundPage = ({ handlePageChange }) => {
  return (
    <div>
      <h2>Playground Page</h2>
      <p>This is the playground page content.</p>
    </div>
  );
};

const NextPageButton = ({ nextPage, handlePageChange }) => {
  return (
    <div style={{ marginTop: "1rem" }}>
      <a>Go to {nextPage.charAt(0).toUpperCase() + nextPage.slice(1)}</a>
      <button
        style={{ marginLeft: "1rem" }}
        onClick={() => handlePageChange(nextPage)}
      >
        Go to {nextPage.charAt(0).toUpperCase() + nextPage.slice(1)}
      </button>
    </div>
  );
};
