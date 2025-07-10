export class InvalidEnvelopeError extends Error {
  constructor(msg = "Invalid KLF envelope format") {
    super(msg);
    this.name = "InvalidEnvelopeError";
  }
}

export class UnauthorizedError extends Error {
  constructor(msg = "Unauthorized KLF request") {
    super(msg);
    this.name = "UnauthorizedError";
  }
}

export class RoutingError extends Error {
  constructor(msg = "Routing failure in KLF pipeline") {
    super(msg);
    this.name = "RoutingError";
  }
} 