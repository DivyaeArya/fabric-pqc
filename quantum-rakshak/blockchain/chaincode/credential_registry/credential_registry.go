// SPDX-License-Identifier: Apache-2.0

package main

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// CredentialRegistryContract provides functions for managing credential metadata.
type CredentialRegistryContract struct {
	contractapi.Contract
}

// CredentialRecord represents the on-chain metadata for a verifiable credential.
type CredentialRecord struct {
	CredentialID   string `json:"credential_id"`
	CredentialHash string `json:"credential_hash"`
	IssuerDID      string `json:"issuer_did"`
	HolderDID      string `json:"holder_did"`
	Status         string `json:"status"` // "active" | "revoked"
	IssuedAt       string `json:"issued_at"`
	RevokedAt      string `json:"revoked_at,omitempty"`
}

// RegisterCredential stores credential metadata on the ledger.
func (c *CredentialRegistryContract) RegisterCredential(
	ctx contractapi.TransactionContextInterface,
	credentialID string,
	credentialHash string,
	issuerDID string,
	holderDID string,
) error {
	// Check if credential already exists
	existing, err := ctx.GetStub().GetState(credentialID)
	if err != nil {
		return fmt.Errorf("failed to read ledger: %v", err)
	}
	if existing != nil {
		return fmt.Errorf("credential %s already exists", credentialID)
	}

	record := CredentialRecord{
		CredentialID:   credentialID,
		CredentialHash: credentialHash,
		IssuerDID:      issuerDID,
		HolderDID:      holderDID,
		Status:         "active",
		IssuedAt:       time.Now().UTC().Format(time.RFC3339),
	}

	recordJSON, err := json.Marshal(record)
	if err != nil {
		return fmt.Errorf("failed to marshal credential record: %v", err)
	}

	return ctx.GetStub().PutState(credentialID, recordJSON)
}

// RevokeCredential updates the credential status to "revoked".
func (c *CredentialRegistryContract) RevokeCredential(
	ctx contractapi.TransactionContextInterface,
	credentialID string,
) error {
	recordJSON, err := ctx.GetStub().GetState(credentialID)
	if err != nil {
		return fmt.Errorf("failed to read ledger: %v", err)
	}
	if recordJSON == nil {
		return fmt.Errorf("credential %s does not exist", credentialID)
	}

	var record CredentialRecord
	if err := json.Unmarshal(recordJSON, &record); err != nil {
		return fmt.Errorf("failed to unmarshal credential record: %v", err)
	}

	record.Status = "revoked"
	record.RevokedAt = time.Now().UTC().Format(time.RFC3339)

	updatedJSON, err := json.Marshal(record)
	if err != nil {
		return fmt.Errorf("failed to marshal updated record: %v", err)
	}

	return ctx.GetStub().PutState(credentialID, updatedJSON)
}

// QueryCredential retrieves credential metadata by ID.
func (c *CredentialRegistryContract) QueryCredential(
	ctx contractapi.TransactionContextInterface,
	credentialID string,
) (*CredentialRecord, error) {
	recordJSON, err := ctx.GetStub().GetState(credentialID)
	if err != nil {
		return nil, fmt.Errorf("failed to read ledger: %v", err)
	}
	if recordJSON == nil {
		return nil, fmt.Errorf("credential %s does not exist", credentialID)
	}

	var record CredentialRecord
	if err := json.Unmarshal(recordJSON, &record); err != nil {
		return nil, fmt.Errorf("failed to unmarshal credential record: %v", err)
	}

	return &record, nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(&CredentialRegistryContract{})
	if err != nil {
		fmt.Printf("Error creating credential registry chaincode: %v\n", err)
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting chaincode: %v\n", err)
	}
}
