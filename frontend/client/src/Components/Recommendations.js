import React, { useState } from "react";
import axios from "axios";
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  List,
  ListItem,
  CircularProgress,
  Alert,
} from "@mui/material";

const Recommendations = () => {
  const [studentId, setStudentId] = useState("");
  const [matches, setMatches] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const getRecommendations = async () => {
    setError(null);
    setLoading(true);
    setMatches([]);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/recommendations",
        {
          student_id: Number(studentId),
          top_k: 6,
        }
      );
      setMatches(response.data.matches);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setError("Failed to fetch recommendations. Please check the student ID.");
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          mt: 6,
          mb: 4,
          p: 3,
          bgcolor: "background.paper",
          borderRadius: 3,
          boxShadow: 2,
        }}
      >
        <Typography variant="h4" align="center" gutterBottom color="primary">
          Student Recommendations 🤝
        </Typography>
        <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
          <TextField
            type="number"
            label="Student ID"
            variant="outlined"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            fullWidth
          />
          <Button
            variant="contained"
            color="primary"
            onClick={getRecommendations}
            disabled={!studentId || loading}
          >
            {loading ? <CircularProgress size={24} /> : "Get Recommendations"}
          </Button>
        </Box>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        {matches.length > 0 && (
          <Box mt={3}>
            <Typography variant="h6" color="secondary" gutterBottom>
              Top Matches:
            </Typography>
            <List>
              {matches.map((match) => (
                <ListItem key={match.id} disablePadding sx={{ mb: 2 }}>
                  <Card sx={{ width: "100%", boxShadow: 3 }}>
                    <CardContent sx={{ display: "flex", justifyContent: "space-between" }}>
                      <Box>
                        <Typography variant="subtitle1" fontWeight="bold" color="primary">
                          {match.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Email: {match.email}
                        </Typography>
                        <Typography variant="body2">
                          GPA: {match.gpa}, Learning: {match.learning_style}
                        </Typography>
                        <Typography variant="body2">
                          Goals: {match.goals && match.goals.join(", ")}
                        </Typography>
                      </Box>
                      <Box
                        sx={{
                          display: "flex",
                          flexDirection: "column",
                          alignItems: "flex-end",
                        }}
                      >
                        <Typography
                          variant="h6"
                          sx={{
                            p: 1,
                            bgcolor: "secondary.light",
                            borderRadius: 1,
                          }}
                        >
                          Score: {match.score.toFixed(2)}
                        </Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </ListItem>
              ))}
            </List>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default Recommendations;
