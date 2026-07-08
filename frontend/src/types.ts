export interface ValidationReport {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
  missing_fields?: string[];
}

export interface ExtractionMetadata {
  filename: string;
  pipeline_time_sec: number;
  ai_metadata?: any;
}

export interface ExtractionResponse {
  success: boolean;
  document: any;
  validation: ValidationReport;
  metadata: ExtractionMetadata;
}
