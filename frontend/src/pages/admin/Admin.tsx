import PageWrapper from "../../components/PageWrapper";
import CSVViewer from "../../components/Admin/CSVViewer";

const AdminPage = () => {
  return (
    <PageWrapper>
      <div className="container mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
        <CSVViewer apiBaseUrl="http://localhost:8000" />
      </div>
    </PageWrapper>
  );
};

export default AdminPage;
