# Set the directory path where your mp4 files are located
$directory = "E:\cornell\2024_awkward\cropped_videos"

# Define the output directory
$outputDirectory = ".\processed"

Write-Output "Searching for mp4 files in directory: $directory"

# Get all mp4 files in the directory and its subfolders
$mp4Files = Get-ChildItem -Path $directory -Filter *.mp4 -Recurse

Write-Output "Found $($mp4Files.Count) mp4 file(s)"

# Loop through each mp4 file and execute the command
foreach ($file in $mp4Files) {
    # Construct the relative path to the mp4 file
    $relativePath = $file.FullName.Replace($directory, "").TrimStart("\")
    $subfolderPath = Split-Path -Path $relativePath -Parent
    $outputPath = Join-Path -Path $outputDirectory -ChildPath $subfolderPath



    # Create the output directory if it doesn't exist
    if (-not (Test-Path -Path $outputPath)) {
        New-Item -ItemType Directory -Path $outputPath | Out-Null
    }

    Write-Output "Processing file: $($file.FullName)"
    Write-Output "Output path: $outputPath"


    # Construct the command with the file path
    $command = ".\FeatureExtraction.exe -f `"$($file.FullName)`" -out_dir  $outputPath"
    Write-Output "COMAND: $command"


    # Execute the command
    Invoke-Expression -Command $command

    Write-Output "Completed processing file: $($file.FullName)"
}

Write-Output "Script execution complete."
