import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";

import LoginPage from "./pages/loginPage.jsx";
import HomePage from "./pages/HomePage";
import SearchPage from "./pages/SearchPage";
import CreateTicketPage from "./pages/CreateTicketPage";
import TicketsBoardPage from "./pages/TicketsBoardPage";
import TicketsKanbanPage from "./pages/TicketsKanbanPage";



function PrivateRoute({ children }) {
  const { isAuthed } = useAuth();
  return isAuthed ? children : <Navigate to="/" replace />;
}

function ClientOnlyRoute({ children }) {
  const { isAuthed, user } = useAuth();
  if (!isAuthed) return <Navigate to="/" replace />;
  if (user?.role !== "client") return <Navigate to="/home" replace />;
  return children;
}

function SeniorEngineerOnlyRoute({ children }) {
  const { isAuthed, user } = useAuth();
  if (!isAuthed) return <Navigate to="/" replace />;

  const ok =
    user?.role === "support" &&
    ["senior", "engineer"].includes(user?.position_team);

  if (!ok) return <Navigate to="/home" replace />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />

      <Route
        path="/home"
        element={
          <PrivateRoute>
            <HomePage />
          </PrivateRoute>
        }
      />

      <Route
        path="/search"
        element={
          <PrivateRoute>
            <SearchPage />
          </PrivateRoute>
        }
      />

      <Route
        path="/tickets/new"
        element={
          <ClientOnlyRoute>
            <CreateTicketPage />
          </ClientOnlyRoute>
        }
      />


      <Route path="*" element={<Navigate to="/" replace />} />

      <Route
        path="/tickets/board"
        element={
          <SeniorEngineerOnlyRoute>
            <TicketsBoardPage />
          </SeniorEngineerOnlyRoute>
        }
      />

      <Route
        path="/tickets/kanban"
        element={
          <SeniorEngineerOnlyRoute>
            <TicketsKanbanPage />
          </SeniorEngineerOnlyRoute>
        }
      />


    </Routes>
  );
}


<Route
  path="/tickets/new"
  element={
    <ClientOnlyRoute>
      <CreateTicketPage />
    </ClientOnlyRoute>
  }
/>

