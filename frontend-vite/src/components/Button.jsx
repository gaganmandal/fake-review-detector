export default function Button({ children, onClick, disabled }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="
        btn-primary w-full mt-3
        text-sm font-medium

        hover:shadow-sm
        active:shadow-inner

        disabled:opacity-50 disabled:cursor-not-allowed
      "
    >
      {children}
    </button>
  );
}
