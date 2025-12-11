import type { FC } from "react";
import type { IStep } from "../RegistrationPage";


const StepName: FC<IStep> = ({
  data,
  setData,
}) => {
  return (
    <div>
      <h2>Как тебя зовут?</h2>
      <input
        type="text"
        value={data.name}
        onChange={(e) => setData({ ...data, name: e.target.value })}
        placeholder="Имя"
      />
    </div>
  );
}

export default StepName
