import type { FC } from "react";
import styles from "./Loader.module.css";


interface LoaderProps {
    text?: string;
}


const Loader: FC<LoaderProps> = ({ text = "Загрузка..." }) => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.indicator} >
                <div className={styles.ring} />
            </div>
            <h2 className={styles.title}>{text}</h2>
        </div>
    );
}

export default Loader;