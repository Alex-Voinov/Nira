import type { FormData } from "@/types/FormData";

type Props = {
  data: FormData;
  setData: (data: FormData) => void;
};

export default function StepCity({ data, setData }: Props) {
  return (
    <div className="step">
      <h2>Город</h2>
      <input
        type="text"
        value={data.city}
        onChange={(e) => setData({ ...data, city: e.target.value })}
        placeholder="Город"
        className="input"
      />
    </div>
  );
}
