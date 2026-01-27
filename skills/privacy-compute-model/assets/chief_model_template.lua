-- Privacy Computing Chief Model
-- Main model that orchestrates multi-party privacy computation

fccall = require("fc_call")

function main()
    -- Context information (optional, for debugging)
    ctx = context()

    -- Define computation type: NORMAL, PSA, PSI, ADD, MUL, AVG, VAR,
    -- INNERPRODUCT, CMP, MEDIAN, MAX, MIN, PSD, PSU, PIR
    local computationType = "{{COMPUTATION_TYPE}}"

    -- Initiator data (optional, depending on computation type)
    local initiatorData = {{INITIATOR_DATA}}

    -- Participant data configurations
    local participantData = {
        {{PARTICIPANT_CONFIGS}}
    }

    -- Execute computation based on type
    if computationType == "NORMAL" then
        -- Normal invoke: plaintext remote call
        return fccall.normalInvoke(participantData[1])

    elseif computationType == "PSA" then
        -- PSA: Privacy-preserving aggregation (+, -, *, /)
        return fccall.psaInvoke(participantData)

    elseif computationType == "ADD" then
        -- Homomorphic addition
        return fccall.addInvoke(participantData)

    elseif computationType == "MUL" then
        -- Homomorphic multiplication
        return fccall.mulInvoke(participantData)

    elseif computationType == "AVG" then
        -- Average computation
        return fccall.avgInvoke(initiatorData, participantData)

    elseif computationType == "VAR" then
        -- Variance computation
        return fccall.varInvoke(initiatorData, participantData)

    elseif computationType == "INNERPRODUCT" then
        -- Inner product
        return fccall.innerproductInvoke(initiatorData, participantData[1])

    elseif computationType == "CMP" then
        -- Comparison
        return fccall.cmpInvoke(initiatorData, participantData[1])

    elseif computationType == "MEDIAN" then
        -- Median computation
        return fccall.medianInvoke(participantData)

    elseif computationType == "MAX" then
        -- Maximum value
        return fccall.maxInvoke(participantData)

    elseif computationType == "MIN" then
        -- Minimum value
        return fccall.minInvoke(participantData)

    elseif computationType == "PSI" then
        -- Intersection (PSI)
        return fccall.psiInvoke(initiatorData, participantData[1])

    elseif computationType == "PSD" then
        -- Difference (PSD)
        return fccall.psdInvoke(initiatorData, participantData[1])

    elseif computationType == "PSU" then
        -- Union (PSU)
        return fccall.psuInvoke(participantData)

    elseif computationType == "PIR" then
        -- Private query (PIR)
        return fccall.pirInvoke(initiatorData, participantData[1])

    elseif computationType == "PIR_PREPROCESS" then
        -- Private query with preprocessing
        return fccall.pirInvokeWithPreprocess(initiatorData, participantData[1])

    else
        error("Unsupported computation type: " .. tostring(computationType))
    end
end
