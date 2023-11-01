open System

// Convert an sbyte to its 8-bit signed binary representation
let sbyteToSignedBinary (x: sbyte) =
    let value = int x // Convert to int for the bit manipulation
    Convert.ToString(value &&& 0b1111_1111, 2).PadLeft(8, '0')

// Helper function to try to parse a string as an sbyte
let tryParseSByte (str: string) =
    match SByte.TryParse(str) with
    | (true, result) -> Some result
    | _ -> None

// Entry point for the program
[<EntryPoint>]
let main argv =
    let results =
        argv
        |> Seq.map tryParseSByte // Use the helper function to try to parse each argument as an sbyte
        |> Seq.choose id // Filter out unsuccessful parses
        |> Seq.map sbyteToSignedBinary // Convert each number to signed binary

    // Print each binary representation
    for binary in results do
        printfn "%s" binary

    0 // Exit code for successful run

// Example usage for testing in F# Interactive or as a script:
// main [| "4"; "-8"; "15"; "-16" |]

