@extends('layouts.app')

@section('content')
    <h1>Reset Password</h1>

    <form method="POST" action="{{ route('password.update') }}">
        @csrf
        <input type="hidden" name="token" value="{{ $token }}">
        <input type="hidden" name="email" value="{{ $email }}">

        <label>New Password</label>
        <input type="password" name="password" required>

        <label>Confirm Password</label>
        <input type="password" name="password_confirmation" required>

        @error('email') <div>{{ $message }}</div> @enderror
        @error('password') <div>{{ $message }}</div> @enderror

        <button type="submit">Reset Password</button>
    </form>
@endsection