import { useEffect, useState, useCallback } from "react";
import { FixedSizeGrid as Grid } from "react-window";

interface CSVFile {
  filename: string;
  size: number;
  uploaded_at: string;
}

interface CSVData {
  headers: string[];
  data: string[][];
  total_rows: number;
  page: number;
  page_size: number;
}

interface CSVViewerProps {
  apiBaseUrl: string;
}

const CSVViewer = ({ apiBaseUrl }: CSVViewerProps) => {
  const [files, setFiles] = useState<CSVFile[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [csvData, setCsvData] = useState<CSVData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch list of CSV files
  const fetchFiles = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${apiBaseUrl}/admin/csv-files`, {
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to fetch CSV files");
      }

      const data = await response.json();
      setFiles(data.files);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl]);

  // Fetch CSV data for a specific file
  const fetchCSVData = useCallback(
    async (filename: string) => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(
          `${apiBaseUrl}/admin/csv-data/${filename}?page=1&page_size=50000`,
          {
            credentials: "include",
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch CSV data");
        }

        const data = await response.json();
        setCsvData(data);
        setSelectedFile(filename);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    },
    [apiBaseUrl]
  );

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]);

  // Format file size
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + " KB";
    return (bytes / (1024 * 1024)).toFixed(2) + " MB";
  };

  // Format date
  const formatDate = (isoString: string): string => {
    const date = new Date(isoString);
    return date.toLocaleString();
  };

  // Cell renderer for react-window
  const Cell = ({
    columnIndex,
    rowIndex,
    style,
  }: {
    columnIndex: number;
    rowIndex: number;
    style: React.CSSProperties;
  }) => {
    if (!csvData) return null;

    const isHeader = rowIndex === 0;
    const content = isHeader
      ? csvData.headers[columnIndex]
      : csvData.data[rowIndex - 1]?.[columnIndex] || "";

    return (
      <div
        style={{
          ...style,
          padding: "8px",
          borderRight: "1px solid #475569",
          borderBottom: "1px solid #475569",
          backgroundColor: isHeader ? "#334155" : "#1e293b",
          color: isHeader ? "#c7d2fe" : "#cbd5e1",
          fontWeight: isHeader ? "bold" : "normal",
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
        }}
        title={content}
      >
        {content}
      </div>
    );
  };

  return (
    <div className="w-full h-full space-y-6">
      <h2 className="text-2xl font-bold text-indigo-400">CSV File Viewer</h2>

      {error && (
        <div className="bg-red-500/10 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {loading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      )}

      {!selectedFile && !loading && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-indigo-400">Available CSV Files</h3>
          {files.length === 0 ? (
            <p className="text-slate-400">No CSV files uploaded yet.</p>
          ) : (
            <div className="grid gap-4">
              {files.map((file) => (
                <div
                  key={file.filename}
                  className="bg-slate-700/50 border border-slate-600 rounded-lg p-4 hover:bg-slate-700 cursor-pointer transition-colors"
                  onClick={() => fetchCSVData(file.filename)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-semibold text-lg text-slate-200">{file.filename}</h4>
                      <p className="text-sm text-slate-400">
                        Size: {formatFileSize(file.size)}
                      </p>
                      <p className="text-sm text-slate-400">
                        Uploaded: {formatDate(file.uploaded_at)}
                      </p>
                    </div>
                    <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors">
                      View Data
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {selectedFile && csvData && !loading && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-xl font-semibold text-indigo-400">{selectedFile}</h3>
              <p className="text-sm text-slate-400">
                Total rows: {csvData.total_rows.toLocaleString()}
              </p>
            </div>
            <button
              onClick={() => {
                setSelectedFile(null);
                setCsvData(null);
              }}
              className="bg-slate-600 hover:bg-slate-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Back to Files
            </button>
          </div>

          <div className="border border-slate-600 rounded-lg overflow-hidden bg-slate-800/50">
            <Grid
              columnCount={csvData.headers.length}
              columnWidth={200}
              height={600}
              rowCount={csvData.data.length + 1} // +1 for header
              rowHeight={40}
              width={Math.min(csvData.headers.length * 200, 1200)}
            >
              {Cell}
            </Grid>
          </div>

          <div className="text-sm text-slate-400">
            Displaying {csvData.data.length.toLocaleString()} of{" "}
            {csvData.total_rows.toLocaleString()} rows
          </div>
        </div>
      )}
    </div>
  );
};

export default CSVViewer;
