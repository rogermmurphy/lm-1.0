export default function ClassDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="games-layout">
      <h1>Class Detail: {params.id}</h1>
      <p>Individual class page for: {params.id}</p>
      <p>This will be enhanced later with full class details.</p>
    </div>
  )
}
