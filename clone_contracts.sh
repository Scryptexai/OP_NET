#!/bin/bash

# Base directory for the smart contract
BASE_DIR="OP_20"

# Array of new token names and symbols
TOKENS=(
    "TokenA:TKA"
    "TokenB:TKB"
    "TokenC:TKC"
    "TokenD:TKD"
    "TokenE:TKE"
    "TokenF:TKF"
    "TokenG:TKG"
    "TokenH:TKH"
    "TokenI:TKI"
    "TokenJ:TKJ"
    "TokenK:TKK"
    "TokenL:TKL"
    "TokenM:TKM"
    "TokenN:TKN"
    "TokenO:TKO"
    "TokenP:TKP"
    "TokenQ:TKQ"
    "TokenR:TKR"
    "TokenS:TKS"
    "TokenT:TKT"
)

# Loop through the tokens and create new contracts
for i in "${!TOKENS[@]}"; do
    TOKEN_NAME=$(echo ${TOKENS[$i]} | cut -d':' -f1)
    TOKEN_SYMBOL=$(echo ${TOKENS[$i]} | cut -d':' -f2)
    CONTRACT_DIR="OP_20_${TOKEN_SYMBOL}"
    CONTRACT_FILE="${TOKEN_NAME}.ts"
    OLD_CONTRACT_NAME="MyToken"
    OLD_TOKEN_NAME="Test"
    OLD_TOKEN_SYMBOL="TEST"

    echo "Creating contract for ${TOKEN_NAME} (${TOKEN_SYMBOL}) in ${CONTRACT_DIR}"

    # Create new directory and copy files
    mkdir -p "${CONTRACT_DIR}/src/contracts"
    cp -r "${BASE_DIR}/src/contracts/MyToken.ts" "${CONTRACT_DIR}/src/contracts/${CONTRACT_FILE}"
    cp "${BASE_DIR}/src/index.ts" "${CONTRACT_DIR}/src/index.ts"
    cp "${BASE_DIR}/src/tsconfig.json" "${CONTRACT_DIR}/src/tsconfig.json"
    cp "${BASE_DIR}/asconfig.json" "${CONTRACT_DIR}/asconfig.json"
    cp "${BASE_DIR}/eslint.config.json" "${CONTRACT_DIR}/eslint.config.json"
    cp "${BASE_DIR}/package.json" "${CONTRACT_DIR}/package.json"
    cp "${BASE_DIR}/tsconfig.json" "${CONTRACT_DIR}/tsconfig.json"

    # Replace content in the new contract file
    sed -i "s/${OLD_CONTRACT_NAME}/${TOKEN_NAME}/g" "${CONTRACT_DIR}/src/contracts/${CONTRACT_FILE}"
    sed -i "s/${OLD_TOKEN_NAME}/${TOKEN_NAME}/g" "${CONTRACT_DIR}/src/contracts/${CONTRACT_FILE}"
    sed -i "s/${OLD_TOKEN_SYMBOL}/${TOKEN_SYMBOL}/g" "${CONTRACT_DIR}/src/contracts/${CONTRACT_FILE}"

    # Replace content in index.ts
    sed -i "s/${OLD_CONTRACT_NAME}/${TOKEN_NAME}/g" "${CONTRACT_DIR}/src/index.ts"
    sed -i "s/MyToken/${TOKEN_NAME}/g" "${CONTRACT_DIR}/src/index.ts"

    # Replace content in asconfig.json
    sed -i "s/MyToken.wasm/${TOKEN_NAME}.wasm/g" "${CONTRACT_DIR}/asconfig.json"

    # Replace content in package.json
    sed -i "s/@btc-vision\/op20/@btc-vision\/${TOKEN_SYMBOL}/g" "${CONTRACT_DIR}/package.json"
    sed -i "s/OP_20 example smart contract/${TOKEN_NAME} (${TOKEN_SYMBOL}) example smart contract/g" "${CONTRACT_DIR}/package.json"
    sed -i "s/MyToken.ts/${CONTRACT_FILE}/g" "${CONTRACT_DIR}/package.json"

    echo "Building ${TOKEN_NAME} (${TOKEN_SYMBOL})..."
    cd "${CONTRACT_DIR}"
    npm install
    npm run build
    cd ..

    echo "Finished building ${TOKEN_NAME} (${TOKEN_SYMBOL})\n"

done

echo "All 20 smart contracts have been cloned and built."

