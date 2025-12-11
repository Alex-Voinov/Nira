import type { FC } from "react";
import type { IStep } from "../RegistrationPage";


const StepAbout: FC<IStep> = ({ data, setData }) => {
  return (
    <div className="step">
      <h2>О себе</h2>
      <textarea
        value={data.description || ''}
        onChange={(e) => setData({ ...data, description: e.target.value })}
        placeholder="Расскажи немного о себе"
        rows={4}
      />
    </div>
  );
}

export default StepAbout