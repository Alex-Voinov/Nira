import type { FC } from "react";
import type { IStep } from "../RegistrationPage";

const StepHeightWeight: FC<IStep> = ({ data, setData }) => {
  return (
    <div className="step">
      <h2>Рост и вес</h2>
      <input
        type="number"
        placeholder="Рост (см)"
        value={data.height ?? ""}
        onChange={(e) => setData({ ...data, height: Number(e.target.value) })}
        className="input"
      />
      <input
        type="number"
        placeholder="Вес (кг)"
        value={data.weight ?? ""}
        onChange={(e) => setData({ ...data, weight: Number(e.target.value) })}
        className="input"
      />
    </div>
  );
}

export default StepHeightWeight;