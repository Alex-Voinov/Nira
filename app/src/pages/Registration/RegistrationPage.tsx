import { useState, type ComponentType } from "react";
import StepName from "./steps/StepName";
import StepAge from "./steps/StepAge";
import StepGender from "./steps/StepGender";
import StepShowGender from "./steps/StepShowGender";
import StepCity from "./steps/StepCity";
import StepHeightWeight from "./steps/StepHeightWeight";
import StepInterests from "./steps/StepInterests";
import StepAbout from "./steps/StepAbout";
import StepSummary from "./steps/StepSummary";
import styles from "./RegistrationPage.module.css";
import { formInitialState, type IUser } from "@/types/user";
import userService from "@/services/userService";
import clsx from 'clsx';


const USERNAME_MIN_LENGTH = 2;

export interface IStep {
  data: IUser;
  setData: (data: IUser) => void;
}

type StepTuple = [ComponentType<IStep>, () => boolean];

export default function RegistrationPage() {
  const [step, setStep] = useState(0);

  const [data, setData] = useState<IUser>(formInitialState);
  const [incorrectStatus, setIncorrectStatus] = useState('')

  const stepComponents: StepTuple[] = [
    [
      StepName,
      () => {
        if (data.name.length >= USERNAME_MIN_LENGTH) return true
        setIncorrectStatus(`Слишком короткое имя`)
        return false
      }
    ],
    [
      StepAge,
      () => { return true }
    ],
    [
      StepGender,
      () => { return true }
    ],
    [
      StepShowGender,
      () => { return true }
    ],
    [
      StepCity,
      () => { return true }
    ],
    [
      StepHeightWeight,
      () => { return true }
    ],
    [
      StepInterests,
      () => { return true }
    ],
    [
      StepAbout,
      () => { return true }
    ],
    [
      StepSummary,
      () => { return true }
    ],
  ];

  const isCorrectInput = stepComponents[step][1]

  const steps = stepComponents.map(([Component, _]) => (
    <Component
      data={data}
      setData={setData}
    />
  ));

  const progress = Math.round(((step + 1) / steps.length) * 100);

  return (
    <div className={styles.wrapper}>
      <form className={clsx(styles.innerWrapper, incorrectStatus && styles.error)}>
        <div className={styles.progressBar}>
          <div className={styles.progress}
            style={{ width: `${progress}%` }}
          />
        </div>
        {steps[step]}
        {step > 0 && <button
          onClick={
            (e) => {
              e.preventDefault();
              setIncorrectStatus('')
              setStep(step - 1);
            }
          }
          type="button"
          className={styles.formButton}
        >
          Назад
        </button>}
        {step < steps.length - 1
          ? <button
            onClick={(e) => {
              e.preventDefault()
              if (!isCorrectInput()) return;
              setStep(step + 1)
              setIncorrectStatus('')
            }}
            className={styles.formButton}
            type="submit"
          >
            Далее
          </button>
          : <button
            className={styles.formButton}
            type="submit"
            onClick={e => {
              e.preventDefault();
              userService.register(data).then(_ => alert('На сервер добавляются обновления по внеделению API Chat GPT')).catch(_ => alert('На сервер добавляются обновления по внеделению API Chat GPT'))
            }}
          >
            Сохранить
          </button>}
        <p>{incorrectStatus}</p>
      </form>
    </div>
  );
}
