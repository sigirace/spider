import { createBrowserRouter } from "react-router-dom";
import Root from "./components/Root";
import Chat from "./components/routes/Chat";
import NotFound from "./components/routes/NotFound";
import Main from "./components/routes/Main";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <NotFound />,
    children: [
      {
        path: "",
        element: <Main />,
      },
      {
        path: ":chatRoomId",
        element: <Chat />,
      },
    ],
  },
]);

export default router;
