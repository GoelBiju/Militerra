import * as React from "react";
import { Card, CardContent, Typography, Box, Chip, Button } from "@mui/material";

export default function MediaCard({ data }) {
  // Directly using `data` as it now contains a single soldier's data
  const soldier = data;
  const healthData = data.health; // Assuming `health` is a direct property of the soldier data

  return (
    <Card
      sx={{
        maxWidth: { xs: 345, sm: 445 },
        m: 2,
        boxShadow: 3,
        borderRadius: 2,
      }}
    >
      <Box sx={{ display: "flex", justifyContent: "center", p: 2 }}>
        <img
          height="150"
          width="150"
          style={{
            borderRadius: "50%",
            objectFit: "cover",
            backgroundPosition: "top",
          }}
          src={soldier.name + ".png"} // Consider updating the src to reflect the soldier's data if applicable
          alt={soldier.name}
        />
      </Box>
      <CardContent>
        <Typography
          gutterBottom
          variant="h5"
          component="div"
          textAlign="center"
        >
          {soldier.name}
        </Typography>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 1,
          }}
        >
          {Object.entries(healthData).map(([key, value], index) => (
            <Chip key={index} label={`${key}: ${value}`} variant="outlined" />
          ))}
        </Box>
        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
          <img
            width={200}
            height={50}
            style={{ borderRadius: "5%" }}
            src="https://media1.tenor.com/m/c6hYp_wGVkgAAAAC/heart-lines.gif"
            alt="Heartbeat animation"
          />
        </Box>
        <Button>Send Support</Button>
      </CardContent>
    </Card>
  );
}
