import type { FC } from "react";
import type { IStep } from "../RegistrationPage";
import styles from './gender.module.css'

const StepGender: FC<IStep> = ({ data, setData }) => {
  const options = [
    { value: "male", label: "Мужской" },
    { value: "female", label: "Женский" },
    { value: "other", label: "Другое" },
  ] as const;

  return (
    <div>
      <h2>Твой пол</h2>
      <div className={styles.selectorsBlock}>
        {options.map(opt => (
          <label key={opt.value} className={styles.option}>
            <input
              type="radio"
              name="gender"
              value={opt.value}
              checked={data.gender === opt.value}
              onChange={() => setData({ ...data, gender: opt.value })}
            />
            <span className={styles.labelText}>{opt.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
};

export default StepGender;
