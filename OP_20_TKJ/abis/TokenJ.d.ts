import { Address, AddressMap } from '@btc-vision/transaction';
import { CallResult, OPNetEvent, IOP_NETContract } from 'opnet';

// ------------------------------------------------------------------
// Event Definitions
// ------------------------------------------------------------------
export type MintEvent = {
    readonly address: Address;
    readonly amount: bigint;
};

// ------------------------------------------------------------------
// Call Results
// ------------------------------------------------------------------

/**
 * @description Represents the result of the mint function call.
 */
export type Mint = CallResult<
    {
        success: boolean;
    },
    OPNetEvent<MintEvent>[]
>;

/**
 * @description Represents the result of the airdrop function call.
 */
export type Airdrop = CallResult<
    {
        success: boolean;
    },
    OPNetEvent<MintEvent>[]
>;

// ------------------------------------------------------------------
// ITokenJ
// ------------------------------------------------------------------
export interface ITokenJ extends IOP_NETContract {
    mint(address: Address, amount: bigint): Promise<Mint>;
    airdrop(addressAndAmount: AddressMap<bigint>): Promise<Airdrop>;
}
