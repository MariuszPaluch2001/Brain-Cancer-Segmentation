import React, {FC, JSX} from "react";

interface Props {
    selector: string;
}
const Gallery: FC<Props> = (props): JSX.Element => {
    return (
        <div>
            <p>{props.selector}</p>
            <div id={props.selector}></div>
        </div>
    );
};

export default Gallery;
