import streamlit as st

st.title("PREOP ASSESSMENT")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
export default function PreAnesthesiaApp() {
  const [age, setAge] = useState(0);
  const [comorbidities, setComorbidities] = useState("");
  const [functionalStatus, setFunctionalStatus] = useState("");
  const [asaClass, setAsaClass] = useState("");
  const [procedureType, setProcedureType] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [history, setHistory] = useState([]);

  const evaluate = async () => {
    const payload = {
      age,
      comorbidities,
      functionalStatus,
      asaClass,
      procedureType
    };

    try {
      const response = await fetch("http://localhost:5000/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const contentType = response.headers.get("content-type");
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      } else if (!contentType || !contentType.includes("application/json")) {
        throw new Error("Invalid JSON response from server");
      }

      const result = await response.json();
      setRecommendations(result.recommendations);
      setHistory((prev) => [
        {
          timestamp: result.timestamp,
          data: payload,
          recommendations: result.recommendations
        },
        ...prev
      ]);
    } catch (error) {
      console.error("Evaluation failed:", error);
      setRecommendations([`Error: ${error.message}`]);
    }
  };

  const downloadSummary = () => {
    const content = `Pre-Anesthesia Evaluation Summary\n\nAge: ${age}\nComorbidities: ${comorbidities}\nFunctional Status: ${functionalStatus}\nASA Class: ${asaClass}\nProcedure Type: ${procedureType}\n\nRecommendations:\n- ${recommendations.join("\n- ")}`;
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `preanesthesia_summary_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-4 sm:p-6 max-w-3xl mx-auto w-full">
      <h1 className="text-2xl font-bold mb-4 text-center">Pre-Anesthesia Testing Tool</h1>

      <Card className="mb-4">
        <CardContent className="space-y-4">
          <Input
            type="number"
            placeholder="Age"
            className="w-full"
            onChange={(e) => setAge(Number(e.target.value))}
          />
          <Textarea
            placeholder="Comorbidities (comma separated: diabetes, CAD, COPD, etc.)"
            className="w-full"
            onChange={(e) => setComorbidities(e.target.value)}
          />
          <Input
            placeholder="Functional status (e.g., METs <4, ADLs)"
            className="w-full"
            onChange={(e) => setFunctionalStatus(e.target.value)}
          />
          <Input
            placeholder="ASA classification (1-4)"
            className="w-full"
            onChange={(e) => setAsaClass(e.target.value)}
          />
          <Input
            placeholder="Procedure type (e.g., vascular, ortho, endoscopy)"
            className="w-full"
            onChange={(e) => setProcedureType(e.target.value.toLowerCase())}
          />
          <div className="flex flex-col sm:flex-row gap-2">
            <Button className="w-full sm:w-auto" onClick={evaluate}>Evaluate</Button>
            <Button className="w-full sm:w-auto" variant="outline" onClick={downloadSummary}>Download Summary</Button>
          </div>
        </CardContent>
      </Card>

      <Card className="mb-4">
        <CardContent>
          <h2 className="text-xl font-semibold mb-2">Recommendations</h2>
          <ul className="list-disc pl-5">
            {recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <h2 className="text-lg font-medium mb-2">Decision History</h2>
          <ul className="list-disc pl-5 space-y-2">
            {history.map((entry, idx) => (
              <li key={idx}>
                <strong>{entry.timestamp}</strong>
                <ul className="list-disc pl-4">
                  {entry.recommendations.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
