
import { useState } from "react";
import {
  LayoutDashboard,
  FlaskConical,
  ChartNoAxesCombined,
  History as HistoryIcon,
  Settings,
  Menu,
  X,
  BrainCircuit
} from "lucide-react";

import Playground from "./pages/Playground";
import Analytics from "./pages/Analytics";
import History from "./pages/History";

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    { name: "Dashboard", icon: LayoutDashboard },
    { name: "Playground", icon: FlaskConical },
    { name: "Analytics", icon: ChartNoAxesCombined },
    { name: "History", icon: HistoryIcon },
    { name: "Settings", icon: Settings }
  ];

  const handleNavigation = (page) => {
    setActivePage(page);
    setSidebarOpen(false);
  };

  return (
    <div className="app-container">
      <aside className={`sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>
        <div className="sidebar-logo">
          <div className="logo-icon">
            <BrainCircuit size={23} />
          </div>

          <div>
            <h2>RAGLab</h2>
            <span>AI Evaluation Studio</span>
          </div>

          <button
            className="close-sidebar"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>

        <div className="sidebar-section">
          <p className="sidebar-label">WORKSPACE</p>

          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`nav-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => handleNavigation(item.name)}
              >
                <Icon size={18} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </div>

        <div className="sidebar-bottom">
          <div className="sidebar-user">
            <div className="user-avatar">R</div>

            <div>
              <h4>RAG Workspace</h4>
              <p>Local Environment</p>
            </div>
          </div>
        </div>
      </aside>

      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}

      <main className="main-content">
        <header className="topbar">
          <button
            className="menu-button"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={21} />
          </button>

          <div className="breadcrumb">
            <span>Workspace</span>
            <span>/</span>
            <strong>{activePage}</strong>
          </div>

          <div className="topbar-right">
            <span className="online-indicator"></span>
            <span>Local Project</span>
          </div>
        </header>

        <div className="page-content">
          {activePage === "Dashboard" && (
            <div className="dashboard-page">
              <div className="page-heading">
                <div>
                  <p className="page-eyebrow">OVERVIEW</p>
                  <h1>Dashboard</h1>
                  <p>Welcome to your RAG evaluation workspace.</p>
                </div>
              </div>

              <div className="dashboard-placeholder">
                <BrainCircuit size={35} />
                <h2>RAGLab Dashboard</h2>
                <p>
                  Your document retrieval and AI model evaluation
                  workspace.
                </p>

                <button
                  onClick={() => setActivePage("Playground")}
                >
                  Open Playground
                </button>
              </div>
            </div>
          )}

          {activePage === "Playground" && <Playground />}

          {activePage === "Analytics" && <Analytics />}

          {activePage === "History" && <History />}

          {activePage === "Settings" && (
            <div className="placeholder-page">
              <h1>Settings</h1>
              <p>Project configuration will be available here.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
