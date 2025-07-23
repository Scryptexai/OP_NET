import { Blockchain } from '@btc-vision/btc-runtime/runtime';
import { TokenD } from './contracts/TokenD';
import { revertOnError } from '@btc-vision/btc-runtime/runtime/abort/abort';

// DO NOT TOUCH TO THIS.
Blockchain.contract = () => {
    // ONLY CHANGE THE CONTRACT CLASS NAME.
    // DO NOT ADD CUSTOM LOGIC HERE.

    return new TokenD();
};

// VERY IMPORTANT
export * from '@btc-vision/btc-runtime/runtime/exports';

// VERY IMPORTANT
export function abort(message: string, fileName: string, line: u32, column: u32): void {
    revertOnError(message, fileName, line, column);
}
